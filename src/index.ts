import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { requestAPI } from './hummingbird-jupyter-pane';

/**
 * Initialization data for the hummingbird-jupyter-pane extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'hummingbird-jupyter-pane',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension hummingbird-jupyter-pane is activated!');

    requestAPI<any>('get_example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The hummingbird_jupyter_pane server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default extension;
