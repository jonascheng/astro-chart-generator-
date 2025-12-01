import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import zhHantTranslation from '../public/locales/zh_Hant/translation.json';

const resources = {
  zh_Hant: {
    translation: zhHantTranslation,
  },
};

i18n.use(initReactI18next).init({
  resources,
  lng: 'zh_Hant', // Default language: Traditional Chinese
  fallbackLng: 'zh_Hant',
  interpolation: {
    escapeValue: false, // React already escapes values
  },
  ns: ['translation'],
  defaultNS: 'translation',
});

export default i18n;
