package main

import (
	"go.uber.org/fx"
	"go.uber.org/fx/fxevent"
	"user/internal/infrastructure/di"
	"user/internal/infrastructure/logger"
	"user/internal/presentation/api"
	"user/internal/presentation/di/config"
)

func main() {
	fx.New(
		fx.WithLogger(func(logger logger.Logger) fxevent.Logger {
			return logger.GetFxLogger()
		}),
		di.Module,
		config.Module,
		api.Module,
	).Run()
}
