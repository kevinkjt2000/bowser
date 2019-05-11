FROM elixir:1.8-alpine@sha256:e8bc436f1c48183638255344a59298f09ef008f8150deb2d4ae0bdfb9ce48829 as builder

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



FROM alpine:latest@sha256:28ef97b8686a0b5399129e9b763d5b7e5ff03576aa5580d6f4182a49c5fe1913

RUN apk --no-cache add \
    bash \
    openssl-dev

WORKDIR /app
COPY --from=builder /opt/built .

CMD ["./bin/bowser", "foreground"]
