# Data Model for Astrological Chart

This document defines the data structure for the JSON object that will be returned by the backend API. This object contains all the necessary information for the frontend to render a complete natal chart.

## `ChartData` Object

The root object will be `ChartData`.

| Field | Type | Description |
|---|---|---|
| `planets` | `[Planet]` | An array of planet objects. |
| `houses` | `[House]` | An array of house cusp objects. |
| `aspects` | `[Aspect]` | An array of aspect objects. |
| `points` | `[Point]` | An array for key astrological points like Ascendant and Midheaven. |

---

### `Planet` Object

Represents a planet or celestial body.

| Field | Type | Description | Example |
|---|---|---|---|
| `name` | `String` | The name of the planet (e.g., "Sun", "Moon"). | `"Sun"` |
| `longitude` | `Number` | The celestial longitude in degrees. | `274.34` |
| `sign` | `String` | The zodiac sign the planet is in. | `"Capricorn"` |
| `degree` | `Number` | The degree within the sign. | `4` |
| `minute` | `Number` | The minute within the degree. | `20` |
| `house` | `Number` | The house number the planet is in. | `3` |

---

### `House` Object

Represents a house cusp.

| Field | Type | Description | Example |
|---|---|---|---|
| `number`| `Number` | The house number (1-12). | `1` |
| `longitude` | `Number` | The celestial longitude of the house cusp in degrees. | `153.25` |
| `sign` | `String` | The zodiac sign the cusp is in. | `"Virgo"` |

---

### `Aspect` Object

Represents an aspect between two planets.

| Field | Type | Description | Example |
|---|---|---|---|
| `planet1` | `String` | The name of the first planet. | `"Sun"` |
| `planet2` | `String` | The name of the second planet. | `"Mars"` |
| `type` | `String` | The type of aspect (e.g., "Conjunction", "Trine", "Square"). | `"Square"` |
| `orb` | `Number` | The orb of the aspect in degrees (how close it is to exact). | `1.2` |

---

### `Point` Object

Represents a key astrological point (AC, MC, etc.).

| Field | Type | Description | Example |
|---|---|---|---|
| `name` | `String` | The name of the point (e.g., "Ascendant", "MC"). | `"Ascendant"` |
| `longitude` | `Number` | The celestial longitude in degrees. | `153.25` |
| `sign` | `String` | The zodiac sign the point is in. | `"Virgo"` |
| `degree` | `Number` | The degree within the sign. | `3` |
| `minute` | `Number` | The minute within the degree. | `15` |

## Example JSON Payload

```json
{
  "planets": [
    {
      "name": "Sun",
      "longitude": 274.34,
      "sign": "Capricorn",
      "degree": 4,
      "minute": 20,
      "house": 3
    },
    {
      "name": "Moon",
      "longitude": 12.5,
      "sign": "Aries",
      "degree": 12,
      "minute": 30,
      "house": 6
    }
  ],
  "houses": [
    {
      "number": 1,
      "longitude": 153.25,
      "sign": "Virgo"
    },
    {
      "number": 2,
      "longitude": 182.0,
      "sign": "Libra"
    }
  ],
  "aspects": [
    {
      "planet1": "Sun",
      "planet2": "Moon",
      "type": "Square",
      "orb": 0.84
    }
  ],
  "points": [
    {
      "name": "Ascendant",
      "longitude": 153.25,
      "sign": "Virgo",
      "degree": 3,
      "minute": 15
    },
    {
      "name": "MC",
      "longitude": 68.0,
      "sign": "Gemini",
      "degree": 8,
      "minute": 0
    }
  ]
}
```
