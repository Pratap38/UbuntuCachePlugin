import GLib from 'gi://GLib';
import Gio from 'gi://Gio';
import Shell from 'gi://Shell';
import {Extension} from 'resource:///org/gnome/shell/extensions/extension.js';

export default class RamGuardianFocusExtension extends Extension {
    enable() {
        this._socketPath = this._resolveSocketPath();
        this._display = global.display;
        this._focusChangedId = this._display.connect(
            'notify::focus-window',
            () => this._logFocusedWindow()
        );

        this._logFocusedWindow();
    }

    disable() {
        if (this._display && this._focusChangedId) {
            this._display.disconnect(this._focusChangedId);
        }

        this._display = null;
        this._focusChangedId = 0;
        this._socketPath = null;
    }

    _logFocusedWindow() {
        const window = this._display?.get_focus_window();

        if (!window) {
            console.log('[RAM Guardian] No focused window');
            return;
        }

        const tracker = Shell.WindowTracker.get_default();
        const app = tracker?.get_window_app(window);
        const appId = app?.get_id?.() ?? '';
        const application = app?.get_name?.() ?? 'Unknown';

        const payload = {
            application,
            app_id: appId,
            pid: window.get_pid?.() ?? -1,
            title: window.get_title?.() ?? '',
            window_id: window.get_id?.() ?? '',
            focused: true,
            timestamp: new Date().toISOString(),
        };

        console.log('[RAM Guardian] Focus changed:', JSON.stringify(payload));
        this._sendPayload(payload);
    }

    _resolveSocketPath() {
        const runtimeDir = GLib.getenv('XDG_RUNTIME_DIR');
        if (runtimeDir) {
            return `${runtimeDir}/ram-guardian-focus.sock`;
        }

        return null;
    }

    _sendPayload(payload) {
        if (!this._socketPath) {
            return;
        }

        try {
            const client = new Gio.SocketClient();
            const address = Gio.UnixSocketAddress.new(this._socketPath);

            client.connect_async(address, null, (_client, result) => {
                try {
                    const connection = client.connect_finish(result);
                    const output = new Gio.DataOutputStream({
                        base_stream: connection.get_output_stream(),
                    });
                    output.put_string(`${JSON.stringify(payload)}\n`, null);
                    connection.close(null);
                } catch (error) {
                    console.log('[RAM Guardian] Socket send failed:', String(error));
                }
            });
        } catch (error) {
            console.log('[RAM Guardian] Socket init failed:', String(error));
        }
    }
}
