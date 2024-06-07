package api

import (
	"context"
	"fmt"
	"go.uber.org/fx"
	"user/internal/infrastructure/db"
	"user/internal/infrastructure/logger"
	"user/internal/presentation/api/config"
	"user/internal/presentation/di/api"
)

var Module = fx.Options(
	api.Module,
	fx.Invoke(Start),
)

func Start(
	lifecycle fx.Lifecycle,
	config config.APIConfig,
	logger logger.Logger,
	pool db.Pool,
) {
	lifecycle.Append(
		fx.Hook{
			OnStart: func(context.Context) error {
				logger.Info(fmt.Sprintf("Starting application on: %d", config.Port))
				go func() {
					defer func() {
						if r := recover(); r != nil {
							logger.Info(fmt.Sprintf("Recovered when boot server, r %s", r))
						}
					}()
					err := pool.Ping(context.Background())
					if err != nil {
						panic(err)
					}
					logger.Info("Successfully pinged databased")
					logger.Info("Application started")
				}()
				return nil
			},
			OnStop: func(context.Context) error {
				logger.Info("Stopping application")
				pool.Close()
				logger.Info("Application stopped")
				return nil
			},
		},
	)
}
