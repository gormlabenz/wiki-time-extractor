type time = 'YYYY-MM-DD' | duration // choose if the event has a duration or not
type duration = { from: 'YYYY-MM-DD'; to: 'YYYY-MM-DD' } // if the event has a duration

type Event = {
  description: string // describe the event
  shortDescription: string // one word that sums up the event
  time: time | duration // the 'YYYY-MM-DD' when the event takes place in time
}

export type timeline = {
  id: string // the id taken from the input JSON
  events: Event[] // A list of events, leave empty if no events are mentioned
}
