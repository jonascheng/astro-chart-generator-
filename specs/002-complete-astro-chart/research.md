# Research & Decisions

This document records the research and technical decisions made during the planning phase for the "Complete Astrological Chart" feature.

## 1. Font Selection for Chart Readability and Fidelity

**Decision**:
- **Chinese Characters**: `Source Han Serif (思源宋體)` will be used for all Chinese text, including labels and titles.
- **Latin Characters & Numerals**: `Source Han Sans` will be used for all non-Chinese text, such as degrees, minutes, and numbers in the positions table.

**Rationale**:
- The goal is to match the reference image (`example-astro.png`) as closely as possible. The font in the image has a traditional, serif-style feel for the Chinese characters, which `Source Han Serif` provides.
- For numerical data and Latin characters, a clean, readable sans-serif font like `Source Han Sans` is ideal and matches the modern aesthetic of the application.
- Both fonts are open-source and provide excellent coverage for Traditional Chinese and Latin character sets, ensuring consistency and avoiding licensing issues.

**Alternatives Considered**:
- Other open-source Chinese fonts like `Open Huninn` were considered but `Source Han Serif` was a better stylistic match for the traditional feel of the reference image.

## 2. Frontend: Chart Rendering with D3.js and React

**Decision**:
The astrological chart will be rendered as an SVG element within a React component. D3.js will be used for the heavy lifting of calculating SVG paths and positions, while React will manage the overall component structure and state.

**Best Practices to Follow**:
1.  **React-Managed SVG**: A React component (e.g., `NatalChart.jsx`) will render the main `<svg>` container. Its dimensions and other high-level properties will be passed as props.
2.  **D3 for Drawing**: Inside this component, `useRef` will be used to get a direct reference to a `<g>` element within the SVG.
3.  **`useEffect` for Logic**: All D3 code for drawing the chart (calculating scales, drawing planet glyphs, aspect lines, house cusps) will be encapsulated within a `useEffect` hook. This hook will re-run whenever the chart data prop changes.
4.  **Data-Driven Approach**: React will fetch the chart data from the backend and pass it as a prop to the `NatalChart` component. D3 will then use this data to generate the visualization.
5.  **Modularity**: D3 is a large library. We will only import the specific modules needed (e.g., `d3-scale`, `d3-shape`) to minimize the bundle size.

**Alternatives Considered**:
- **Canvas**: While potentially more performant for a very high number of elements, SVG provides better scalability, easier interactivity (event handling on individual elements), and is generally crisper for this type of detailed diagram.
- **Pure React SVG**: Manually creating all SVG elements in JSX is possible but would be extremely verbose and complex, losing the powerful data-to-visual mapping capabilities of D3.

## 3. Backend: Astrological Calculations with `pyswisseph`

**Decision**:
The Python backend will use the `pyswisseph` library to perform all astrological calculations.

**Implementation Details**:
1.  **Ephemeris Files**: The required Swiss Ephemeris data files will be downloaded from the AstroDienst FTP server and stored in a designated directory accessible to the backend application. The path to these files will be configured using `swe.set_ephe_path()`.
2.  **Calculations**: The backend will expose an API endpoint that takes birth date, time, and location. It will use `pyswisseph` to:
    -   Convert the birth date/time to a Julian Day number (`swe.utc_to_jd`).
    -   Calculate planetary and other celestial body positions (`swe.calc_ut`).
    -   Calculate house cusps (`swe.houses_ex`).
    -   Manually calculate aspects by finding the angular difference between planetary longitudes.
3.  **Timezone Handling**: Timezone conversion is critical for accuracy. The frontend will send UTC-adjusted date and time to the backend, or the backend will perform the conversion based on the user's selected location.

**Alternatives Considered**:
- **Other Python Libraries**: Other libraries exist, but `pyswisseph` is a direct and widely trusted wrapper for the Swiss Ephemeris, which is the industry standard for accuracy.

## 4. Frontend: Internationalization (i18n)

**Decision**:
The `react-i18next` library will be used to handle the translation of the user interface into Traditional Chinese.

**Implementation Details**:
1.  **Configuration**: An `i18n.js` file will be created to configure `react-i18next`, including setting up the language resources.
2.  **Translation Files**: Translation strings will be stored in JSON format in `public/locales/zh_Hant/translation.json`.
3.  **Component Integration**: The `useTranslation` hook will be used within React components to access the translation function (`t`) and translated strings.
4.  **App Wrapper**: The root `App` component will be wrapped in the `<I18nextProvider>` to make the i18n instance available throughout the component tree.

**Alternatives Considered**:
- **Manual String Management**: Managing translations manually with simple objects is feasible for a very small app but quickly becomes unmanageable. `react-i18next` provides a robust framework for handling translations, plurals, and language changes.
