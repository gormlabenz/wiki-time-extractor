type time = Date | duration // choose if the event has a duration or not
type duration = { from: Date; to: Date } // if the event has a duration

type Event = {
  description: string // describe the event
  conclusionWord: string // one word that sums up the event
  time: time | duration // the date when the event takes place in time
}

export type timeline = {
  id: string // the id taken from the input JSON
  events: Event[] // A list of events, leave empty if no events are mentioned
}
