package di

import (
	"go.uber.org/fx"
	"user/internal/infrastructure/di/db"
	"user/internal/infrastructure/di/logger"
)

var Module = fx.Module(
	"infrastructure.di",
	fx.Options(
		db.Module,
		logger.Module,
	),
)
