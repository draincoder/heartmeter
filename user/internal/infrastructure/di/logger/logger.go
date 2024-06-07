package logger

import (
	"go.uber.org/fx"
	"user/internal/infrastructure/logger"
)

var Module = fx.Provide(
	logger.NewLogger,
)
