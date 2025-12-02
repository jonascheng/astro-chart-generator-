import PropTypes from 'prop-types';
import { useTranslation } from 'react-i18next';
import './PositionsTable.css';

/**
 * Positions Table component.
 * Displays planetary and point positions in a comprehensive table format,
 * organized by celestial body with their zodiac signs and precise coordinates.
 */
export default function PositionsTable({ planets, points }) {
  const { t } = useTranslation();
  
  if (!planets && !points) {
    return null;
  }

  const planetsData = planets || [];
  const pointsData = points || [];

  // Combine planets and points for a unified table display
  const allBodies = [
    ...planetsData.map((p) => ({
      ...p,
      type: 'planet',
    })),
    ...pointsData.map((p) => ({
      ...p,
      type: 'point',
    })),
  ];

  // Sort by longitude for a natural celestial order
  allBodies.sort((a, b) => a.longitude - b.longitude);

  return (
    <div className="positions-table-container">
      <h3>{t('table_title')}</h3>
      <div className="table-wrapper">
        <table className="positions-table">
          <thead>
            <tr>
              <th>{t('table_header_name')}</th>
              <th>{t('table_header_sign')}</th>
              <th>Position</th>
              <th>Longitude</th>
              {planetsData.length > 0 && <th>{t('table_header_house')}</th>}
            </tr>
          </thead>
          <tbody>
            {allBodies.map((body) => (
              <tr key={`${body.type}-${body.name}`} className={`body-row body-${body.type}`}>
                <td className="body-name">{body.name}</td>
                <td className="body-sign">{body.sign}</td>
                <td className="body-position">
                  {body.degree}°{body.minute}'
                </td>
                <td className="body-longitude">{body.longitude.toFixed(2)}°</td>
                {planetsData.length > 0 && (
                  <td className="body-house">
                    {body.house ? `House ${body.house}` : '—'}
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="table-legend">
        <p className="legend-item">
          <span className="legend-marker planet-marker">●</span>
          {' '}
          {t('chart_title')}
        </p>
        <p className="legend-item">
          <span className="legend-marker point-marker">◆</span>
          {' '}
          Astrological Points
        </p>
      </div>
    </div>
  );
}

PositionsTable.propTypes = {
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
  points: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      sign: PropTypes.string.isRequired,
      degree: PropTypes.number.isRequired,
      minute: PropTypes.number.isRequired,
      longitude: PropTypes.number.isRequired,
    })
  ),
};

PositionsTable.defaultProps = {
  planets: [],
  points: [],
};
