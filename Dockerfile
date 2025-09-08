ARG APP_NAME=bowser
ARG MIX_ENV=prod

FROM elixir:1.9-alpine@sha256:9a59d8610699c0e98096eaa8c7f4a6e92382e96ec355bd784cd575e37ad1b9c4 as builder

ARG APP_NAME
ARG COOKIE
ARG MIX_ENV

RUN apk --no-cache add \
    git

RUN mix local.hex --force && \
    mix local.rebar --force && \
    mix hex.info

WORKDIR /app
COPY mix.* ./
RUN mix do deps.get --only prod, deps.compile
COPY lib lib
COPY config config
RUN mix release



FROM alpine:3.11@sha256:a0ce0e57c6900f6f13cee6f1c1e0337cedd745ebc1bac226c61eb574667c6d04 as production

ARG APP_NAME
ARG MIX_ENV

RUN apk --no-cache add \
    bash \
    openssl-dev

WORKDIR /app
COPY --from=builder /app/_build/${MIX_ENV}/rel/${APP_NAME} .

CMD ["./bin/bowser", "start"]
