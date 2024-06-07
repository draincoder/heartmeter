package db

import (
	"go.uber.org/fx"
	"user/internal/application/persistence"
	"user/internal/infrastructure/db"
	"user/internal/infrastructure/db/uow"
)

var Module = fx.Provide(
	fx.Annotate(
		uow.NewUoWManager,
		fx.As(new(persistence.UoWManager)),
	),
	db.NewPool,
)
