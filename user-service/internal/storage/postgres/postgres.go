package postgres

import (
	"database/sql"
	"fmt"
	_ "github.com/jackc/pgx/v5/stdlib"
	"user-service/internal/config"
)

type Storage struct {
	DB *sql.DB
}

func New(cfg config.DBConfig) (*Storage, error) {
	const op = "storage.postgres.New"

	db, err := sql.Open("pgx", cfg.RenderURL())
	if err != nil {
		return nil, fmt.Errorf("%s: %w", op, err)
	}

	err = db.Ping()
	if err != nil {
		return nil, fmt.Errorf("%s: %w", op, err)
	}

	return &Storage{DB: db}, nil
}
