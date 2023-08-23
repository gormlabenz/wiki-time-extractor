type time = Date | duration
type duration = { from: Date; to: Date }

type pointInTime = {
  description: string
  conclusionWord: string
  time: time
}

export type timeline = {
  title: string
  description: string
  coordinates: [number, number]
  points: pointInTime[]
}
