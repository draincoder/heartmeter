package db

import (
	"context"
	"github.com/jackc/pgx/v5/pgxpool"
	"user/internal/infrastructure/db/config"
)

type Pool struct {
	*pgxpool.Pool
}

func NewPool(config config.DBConfig) Pool {
	conn, err := pgxpool.New(context.Background(), config.RenderURL())
	if err != nil {
		panic(err)
	}
	conn.Config().MaxConns = int32(config.MaxIdleConnection) // TODO: More settings
	return Pool{Pool: conn}
}
