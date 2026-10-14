import type { ConfigType } from '@plone/registry';
import PresenterView from '../components/Presenter/PresenterView';

export default function install(config: ConfigType) {
  // Replaces the view registered by @plone-collective/volto-techevent.
  config.views.contentTypesViews = {
    ...config.views.contentTypesViews,
    Presenter: PresenterView,
  };

  return config;
}
