FROM elixir:1.8-alpine@sha256:d8b038d2e06cf8209ade85e946c0f878e704a24367e84c830b03d92ecb6fe7a8 as builder

ARG APP_NAME=bowser
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



FROM alpine:latest@sha256:6a92cd1fcdc8d8cdec60f33dda4db2cb1fcdcacf3410a8e05b3741f44a9b5998

RUN apk --no-cache add \
    bash \
    openssl-dev

WORKDIR /app
COPY --from=builder /opt/built .

CMD ["./bin/bowser", "foreground"]
