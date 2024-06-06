package postgres

import (
	"database/sql"
	"fmt"
	_ "github.com/jackc/pgx/v5/stdlib"
	"user-service/internal/config"
)

type Storage struct {
	db *sql.DB
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

	return &Storage{db: db}, nil
}

func (s *Storage) Close() error {
	return s.db.Close()
}
