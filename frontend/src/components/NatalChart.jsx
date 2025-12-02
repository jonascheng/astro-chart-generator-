import PropTypes from 'prop-types';
import { useTranslation } from 'react-i18next';
import './NatalChart.css';

/**
 * Natal Chart visualization component.
 * Displays planetary positions, houses, and aspects in a circular chart format.
 */
export default function NatalChart({ chartData }) {
  const { t } = useTranslation();

  if (!chartData) {
    return null;
  }

  const { planets, houses, aspects, points } = chartData;

  const CHART_SIZE = 400;
  const CENTER = CHART_SIZE / 2;
  const OUTER_RADIUS = 150;
  const INNER_RADIUS = 80;

  const ZODIAC_SIGNS = [
    'Aries',
    'Taurus',
    'Gemini',
    'Cancer',
    'Leo',
    'Virgo',
    'Libra',
    'Scorpio',
    'Sagittarius',
    'Capricorn',
    'Aquarius',
    'Pisces',
  ];

  const ZODIAC_SYMBOLS = {
    Aries: '♈',
    Taurus: '♉',
    Gemini: '♊',
    Cancer: '♋',
    Leo: '♌',
    Virgo: '♍',
    Libra: '♎',
    Scorpio: '♏',
    Sagittarius: '♐',
    Capricorn: '♑',
    Aquarius: '♒',
    Pisces: '♓',
  };

  const PLANET_SYMBOLS = {
    Sun: '☉',
    Moon: '☽',
    Mercury: '☿',
    Venus: '♀',
    Mars: '♂',
    Jupiter: '♃',
    Saturn: '♄',
    Uranus: '♅',
    Neptune: '♆',
    Pluto: '♇',
  };

  /**
   * Convert zodiac position to SVG coordinates.
   * 0 degrees = right (3 o'clock), increases counter-clockwise.
   */
  const getCoordinates = (degrees, radius) => {
    // Convert to radians (0 degrees starts at right, go counter-clockwise)
    const radians = ((degrees * 30 - 90) * Math.PI) / 180;
    const x = CENTER + radius * Math.cos(radians);
    const y = CENTER + radius * Math.sin(radians);
    return { x, y };
  };

  // Calculate planet positions
  const planetPositions = planets.map((planet) => {
    // Use longitude directly if available, otherwise calculate from sign and degree
    const degrees = planet.longitude || (planet.degree + (ZODIAC_SIGNS.indexOf(planet.sign) * 30 || 0));
    const coords = getCoordinates(degrees % 360, OUTER_RADIUS - 30);
    return { ...planet, ...coords, degrees: degrees % 360 };
  });

  // Calculate house cusps
  const houseCusps = houses.map((house) => {
    // Use longitude directly if available, otherwise calculate from sign and degrees
    const degrees = house.longitude || (house.degree + (ZODIAC_SIGNS.indexOf(house.sign) * 30 || 0));
    return { ...house, degrees: degrees % 360 };
  });

  const planetsList = planets
    .map((p) => `${p.name} in ${p.sign}`)
    .join(', ');
  const aspectsList = aspects
    .map((a) => `${a.planet1} ${a.type} ${a.planet2}`)
    .join(', ');

  return (
    <div className="natal-chart-container">
      <h3>Your Natal Chart</h3>
      <svg
        width={CHART_SIZE}
        height={CHART_SIZE}
        className="natal-chart-svg"
        role="img"
        aria-label={`Natal chart with planets: ${planetsList}${aspectsList ? `. Aspects: ${aspectsList}` : ''}`}
      >
        {/* Background circle */}
        <circle cx={CENTER} cy={CENTER} r={OUTER_RADIUS} className="chart-bg" />

        {/* Zodiac signs ring */}
        {ZODIAC_SIGNS.map((sign, i) => {
          const angle = (i * 30 + 15) * (Math.PI / 180);
          const radius = OUTER_RADIUS + 20;
          const x = CENTER + radius * Math.cos(angle - Math.PI / 2);
          const y = CENTER + radius * Math.sin(angle - Math.PI / 2);

          return (
            <text
              key={`zodiac-${sign}`}
              x={x}
              y={y}
              className="zodiac-symbol"
              textAnchor="middle"
              dominantBaseline="middle"
              aria-label={sign}
            >
              {ZODIAC_SYMBOLS[sign]}
            </text>
          );
        })}

        {/* House cusps lines */}
        {houseCusps.map((house) => {
          const coords = getCoordinates(house.degrees, OUTER_RADIUS);
          return (
            <line
              key={`house-line-${house.number}`}
              x1={CENTER}
              y1={CENTER}
              x2={coords.x}
              y2={coords.y}
              className="house-line"
              aria-label={`House ${house.number}`}
            />
          );
        })}

        {/* House numbers */}
        {houseCusps.map((house) => {
          const coords = getCoordinates(house.degrees, INNER_RADIUS);
          return (
            <text
              key={`house-num-${house.number}`}
              x={coords.x}
              y={coords.y}
              className="house-number"
              textAnchor="middle"
              dominantBaseline="middle"
            >
              {house.number}
            </text>
          );
        })}

        {/* Planets */}
        {planetPositions.map((planet) => (
          <g
            key={`planet-${planet.name}`}
            className="planet"
            tabIndex="0"
            role="button"
            aria-label={`${planet.name} at ${planet.degree}°${planet.minute}' in ${planet.sign}`}
          >
            <circle
              cx={planet.x}
              cy={planet.y}
              r={8}
              className="planet-circle"
            />
            <text
              x={planet.x}
              y={planet.y}
              className="planet-symbol"
              textAnchor="middle"
              dominantBaseline="middle"
              aria-hidden="true"
            >
              {PLANET_SYMBOLS[planet.name] || planet.name[0]}
            </text>
          </g>
        ))}

        {/* Center point */}
        <circle cx={CENTER} cy={CENTER} r={3} className="center-point" />
      </svg>

      {/* Legend */}
      <div className="chart-legend">
        <section className="legend-section">
          <h4>Planets & Signs</h4>
          <ul>
            {planets.map((planet) => (
              <li key={planet.name}>
                <span className="planet-symbol" aria-hidden="true">
                  {PLANET_SYMBOLS[planet.name]}
                </span>
                <strong>{planet.name}</strong>: {planet.sign} {planet.degree}°{planet.minute}'
              </li>
            ))}
          </ul>
        </section>

        {aspects.length > 0 && (
          <section className="legend-section">
            <h4>Major Aspects</h4>
            <ul>
              {aspects.map((aspect, i) => (
                <li key={`aspect-${i}`}>
                  <strong>{aspect.planet1}</strong> {aspect.type}{' '}
                  <strong>{aspect.planet2}</strong>
                  <br />
                  <small>Orb: {aspect.orb.toFixed(2)}°</small>
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>
    </div>
  );
}

NatalChart.propTypes = {
  chartData: PropTypes.shape({
    planets: PropTypes.arrayOf(
      PropTypes.shape({
        name: PropTypes.string.isRequired,
        sign: PropTypes.string.isRequired,
        degree: PropTypes.number.isRequired,
        minute: PropTypes.number.isRequired,
        longitude: PropTypes.number.isRequired,
        house: PropTypes.number.isRequired,
      })
    ),
    houses: PropTypes.arrayOf(
      PropTypes.shape({
        number: PropTypes.number.isRequired,
        sign: PropTypes.string.isRequired,
        longitude: PropTypes.number.isRequired,
      })
    ),
    points: PropTypes.arrayOf(
      PropTypes.shape({
        name: PropTypes.string.isRequired,
        sign: PropTypes.string.isRequired,
        degree: PropTypes.number.isRequired,
        minute: PropTypes.number.isRequired,
        longitude: PropTypes.number.isRequired,
      })
    ),
    aspects: PropTypes.arrayOf(
      PropTypes.shape({
        type: PropTypes.string.isRequired,
        planet1: PropTypes.string.isRequired,
        planet2: PropTypes.string.isRequired,
        orb: PropTypes.number.isRequired,
      })
    ),
  }),
};
