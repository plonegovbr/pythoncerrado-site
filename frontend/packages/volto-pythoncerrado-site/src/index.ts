import type { ConfigType } from '@plone/registry';
import installSettings from './config/settings';
import installViews from './config/views';

// Outfit, the font of every Python Cerrado 2026 theme record
// (`font_family_primary` / `font_family_secondary`). Loaded once here, from
// the package rather than Google Fonts, so pages make no third-party request.
import '@fontsource/outfit/300.css';
import '@fontsource/outfit/400.css';
import '@fontsource/outfit/500.css';
import '@fontsource/outfit/600.css';
import '@fontsource/outfit/700.css';

function applyConfig(config: ConfigType) {
  installSettings(config);
  installViews(config);

  return config;
}

export default applyConfig;
