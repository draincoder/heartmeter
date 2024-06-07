package config

import (
	"go.uber.org/fx"
	"user/internal/presentation/config"
)

var Module = fx.Module(
	"presentation.config",
	fx.Provide(
		config.NewConfig,
		config.NewDBConfig,
		config.NewAPIConfig,
		config.NewLoggerConfig,
	),
)
