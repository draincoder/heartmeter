package uow

import (
	"context"
	"github.com/jackc/pgx/v5"
	"user/internal/application/persistence"
	"user/internal/infrastructure/db"
)

type UoW struct {
	Pool db.Pool
	Tx   pgx.Tx
}

func (u *UoW) Commit() error {
	return u.Tx.Commit(context.Background())
}

func (u *UoW) Rollback() error {
	err := u.Tx.Rollback(context.Background())
	if err != nil {
		return err
	}
	return nil
}

func (u *UoW) Begin() (interface{}, error) {
	tx, err := u.Pool.Begin(context.Background())
	if err != nil {
		return nil, err
	}
	u.Tx = tx
	return u.Tx, nil
}

type UoWManager struct {
	Pool db.Pool
}

func (u *UoWManager) GetUoW() persistence.UoW {
	return &UoW{
		Pool: u.Pool,
	}
}

func NewUoWManager(pool db.Pool) *UoWManager {
	return &UoWManager{
		Pool: pool,
	}
}
