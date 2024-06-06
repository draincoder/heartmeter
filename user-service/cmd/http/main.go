package main

import (
	"lib/slogger"
	"log/slog"
	"os"
	"user-service/internal/config"
	"user-service/internal/storage/postgres"
)

func setupLogger(cfg config.LogConfig) *slog.Logger {
	var logger *slog.Logger

	if cfg.RenderJSON {
		logger = slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: cfg.Level}))
	} else {
		logger = slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: cfg.Level}))
	}

	return logger
}

func main() {
	cfg := config.MustLoad()
	logger := setupLogger(cfg.Log)

	logger.Info("Config loaded")

	storage, err := postgres.New(cfg.DB)
	if err != nil {
		logger.Error("Failed to initialize storage", slogger.Err(err))
		os.Exit(1)
	}
	defer func() {
		err = storage.Close()
		if err != nil {
			logger.Error("Failed to close storage", slogger.Err(err))
		} else {
			logger.Info("Storage closed successfully")
		}
	}()

	logger.Info("Database initialized successfully")

	// TODO: ini router - chi/echo, "chi render"
	// TODO: run server
}
