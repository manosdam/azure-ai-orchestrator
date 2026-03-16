import { BootstrapContext, bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app'; // <--- Εδώ είναι η διόρθωση
import { config } from './app/app.config.server';

const bootstrap = (context: BootstrapContext) =>
    bootstrapApplication(AppComponent, config, context); // <--- Και εδώ

export default bootstrap;