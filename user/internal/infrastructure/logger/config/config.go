package config

type LoggerConfig struct {
	Level      string `toml:"level"`
	RenderJson bool   `toml:"render_json"`
}
