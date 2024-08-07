package events

import (
	"encoding/json"
	"github.com/google/uuid"
	"time"
)

type Event interface {
	Bytes() ([]byte, error)
	UniqueAggregateID() uuid.UUID
}

type BaseEvent struct {
	EventID        uuid.UUID `json:"event_id,omitempty"`
	EventType      string    `json:"event_type"`
	EventTimestamp time.Time `json:"event_timestamp,omitempty"`
}

func (BaseEvent) Create(eventType string) BaseEvent {
	return BaseEvent{
		EventType:      eventType,
		EventID:        uuid.New(),
		EventTimestamp: time.Now(),
	}
}
func Bytes(v any) ([]byte, error) {
	bin, err := json.Marshal(v)
	if err != nil {
		return nil, err
	}
	return bin, nil
}
func (o *BaseEvent) Bytes() ([]byte, error) {
	return Bytes(o)
}
func (o *BaseEvent) UniqueAggregateID() uuid.UUID {
	return o.EventID
}
