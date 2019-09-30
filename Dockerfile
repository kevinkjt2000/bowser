ARG APP_NAME=bowser

FROM elixir:1.9-alpine@sha256:cdf3e9e7ea3c076b3780a0963c16f0e7cb6f8abe6c8e160618e73049ac61585e as builder

ARG APP_NAME
ARG COOKIE
ARG MIX_ENV=prod

RUN apk --no-cache add \
    git

RUN mix local.hex --force && \
    mix local.rebar --force && \
    mix hex.info

WORKDIR /app
COPY mix.* ./
RUN mix do deps.get --only prod, deps.compile
COPY . .
RUN mix release --verbose --env=${MIX_ENV} && \
    mkdir -p /opt/built && \
    cp _build/${MIX_ENV}/rel/${APP_NAME}/releases/*/${APP_NAME}.tar.gz /opt/built && \
    cd /opt/built && \
    tar -xzf ${APP_NAME}.tar.gz && \
    rm ${APP_NAME}.tar.gz



FROM alpine:3.10@sha256:acd3ca9941a85e8ed16515bfc5328e4e2f8c128caa72959a58a127b7801ee01f as production

ARG APP_NAME

RUN apk --no-cache add \
    bash \
    openssl-dev

WORKDIR /app
COPY --from=builder /opt/built .

CMD ["./bin/${APP_NAME}", "foreground"]
