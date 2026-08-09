import GLib from 'gi://GLib';
import Gio from 'gi://Gio';
import Shell from 'gi://Shell';

import {
    Extension,
} from 'resource:///org/gnome/shell/extensions/extension.js';


export default class RamGuardianFocusExtension extends Extension {

    enable() {
        this._socketPath = this._resolveSocketPath();
        this._socketClients = new Set();
        this._display = global.display;

        this._focusChangedId = this._display.connect(
            'notify::focus-window',
            () => this._handleFocusChanged()
        );

        // Send the currently focused window immediately.
        this._handleFocusChanged();
    }

    disable() {
        if (this._display && this._focusChangedId) {
            this._display.disconnect(this._focusChangedId);
        }

        if (this._socketClients) {
            this._socketClients.clear();
        }

        this._display = null;
        this._focusChangedId = 0;
        this._socketPath = null;
        this._socketClients = null;
    }

    // ---------------------------------------------------------
    // Focus Handling
    // ---------------------------------------------------------

    _handleFocusChanged() {
        const window = this._display?.get_focus_window();

        if (!window) {
            console.log('[RAM Guardian] No focused window');
            return;
        }

        const tracker = Shell.WindowTracker.get_default();
        const app = tracker?.get_window_app(window);

        const payload = {
            application: app?.get_name?.() ?? 'Unknown',
            app_id: app?.get_id?.() ?? '',
            pid: window.get_pid?.() ?? -1,
            title: window.get_title?.() ?? '',
            window_id: window.get_id?.() ?? '',
            focused: true,
            timestamp: new Date().toISOString(),
        };

        console.log(
            '[RAM Guardian] Focus changed:',
            JSON.stringify(payload)
        );

        this._sendPayload(payload);
    }

    // ---------------------------------------------------------
    // Socket Path
    // ---------------------------------------------------------

    _resolveSocketPath() {
        /*
         * Prefer GLib's runtime directory instead of depending
         * only on XDG_RUNTIME_DIR being present in GNOME Shell's
         * environment.
         */
        const runtimeDir = GLib.get_user_runtime_dir();

        if (runtimeDir) {
            return `${runtimeDir}/ram-guardian-focus.sock`;
        }

        const envRuntimeDir = GLib.getenv('XDG_RUNTIME_DIR');

        if (envRuntimeDir) {
            return `${envRuntimeDir}/ram-guardian-focus.sock`;
        }

        console.log(
            '[RAM Guardian] Unable to determine runtime directory'
        );

        return null;
    }

    // ---------------------------------------------------------
    // IPC
    // ---------------------------------------------------------

   _sendPayload(payload) {
        if (!this._socketPath) {
            console.log(
                '[RAM Guardian] ERROR: Focus socket path unavailable'
            );
            return;
        }

        console.log(
            '[RAM Guardian] IPC: attempting connection to:',
            this._socketPath
        );

        const client = new Gio.SocketClient();

        /*
         * Keep the client alive until the async operation finishes.
         */
        this._socketClients.add(client);

        const address = Gio.UnixSocketAddress.new(
            this._socketPath
        );

        console.log(
            '[RAM Guardian] IPC: Unix socket address created'
        );

        client.connect_async(
            address,
            null,
            (source, result) => {
                console.log(
                    '[RAM Guardian] IPC: connect callback reached'
                );

                try {
                    const connection = source.connect_finish(result);

                    console.log(
                        '[RAM Guardian] IPC: connection established'
                    );

                    const output = new Gio.DataOutputStream({
                        base_stream: connection.get_output_stream(),
                    });

                    const message =
                        `${JSON.stringify(payload)}\n`;

                    console.log(
                        '[RAM Guardian] IPC: sending payload'
                    );

                    output.put_string(message, null);

                    console.log(
                        '[RAM Guardian] IPC: payload written'
                    );

                    output.flush(null);

                    console.log(
                        '[RAM Guardian] IPC: payload flushed successfully'
                    );

                    output.close(null);
                    connection.close(null);

                    console.log(
                        '[RAM Guardian] IPC: connection closed'
                    );

                } catch (error) {
                    console.log(
                        '[RAM Guardian] IPC ERROR:',
                        String(error)
                    );
                } finally {
                    this._socketClients.delete(source);

                    console.log(
                        '[RAM Guardian] IPC: client released'
                    );
                }
            }
        );
    }
}
