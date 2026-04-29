document.addEventListener("DOMContentLoaded", function() {
    // 1. Obtener las imágenes desde el HTML
    const imagenesJson = document.getElementById('datos-imagenes');
    if (!imagenesJson) return; // Si no estamos en el index, no hace nada

    const listaImagenes = JSON.parse(imagenesJson.textContent);
    const hero = document.querySelector('.hero-section');
    let indiceActual = 0;

    // 2. Función para cambiar la imagen con efecto
    function cambiarImagen() {
        indiceActual = (indiceActual + 1) % listaImagenes.length;
        hero.classList.add('hero-dark');
        setTimeout(() => {
            hero.style.backgroundImage = `linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('${listaImagenes[indiceActual]}')`;
            hero.classList.remove('hero-dark');
        }, 800);
    }

    // 3. Iniciar el ciclo cada 15 segundos
    if (hero && listaImagenes.length > 0) {
        setInterval(cambiarImagen, 15000);
    }
});

/* ============================================================
   LÓGICA DEL PANEL DE ACCESIBILIDAD
   ============================================================ */

'use strict';
(function() {
    const state = {
        panelOpen: false,
        activeTab: 'visual',
        theme: 'default',
        filter: 'none',
        font: 'sans',
        spacing: 'normal',
        fontSize: 100,
        brightness: 100,
        width: 860,
        lightTheme: false,
        features: {
            'big-cursor': false,
            'show-focus': false,
            'highlight-links': false,
            'no-motion': false
        }
    };

    function save(k, v) {
        try { localStorage.setItem('a11y_' + k, JSON.stringify(v)); } catch (e) {}
    }

    function load(k, def) {
        try {
            const v = localStorage.getItem('a11y_' + k);
            return v !== null ? JSON.parse(v) : def;
        } catch (e) { return def; }
    }

    let toastTimer;

    function toast(msg) {
        const el = document.getElementById('a11y-toast');
        const txt = document.getElementById('a11y-toast-msg');
        if (!el || !txt) return;
        txt.textContent = msg;
        el.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => el.classList.remove('show'), 2200);
    }

    function togglePanel() {
        state.panelOpen = !state.panelOpen;
        const panel = document.getElementById('a11y-panel');
        const btn = document.getElementById('a11y-btn');
        if (!panel || !btn) return;
        panel.classList.toggle('open', state.panelOpen);
        btn.setAttribute('aria-expanded', String(state.panelOpen));
        if (state.panelOpen) {
            const firstTab = panel.querySelector('.a11y-panel-tab.active');
            if (firstTab) firstTab.focus();
        }
    }

    function closePanel() {
        state.panelOpen = false;
        const panel = document.getElementById('a11y-panel');
        const btn = document.getElementById('a11y-btn');
        if (panel) panel.classList.remove('open');
        if (btn) btn.setAttribute('aria-expanded', 'false');
    }

    function switchTab(name) {
        state.activeTab = name;
        document.querySelectorAll('.a11y-tab-content').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.a11y-panel-tab').forEach(t => t.classList.remove('active'));
        const content = document.getElementById('a11y-tab-' + name);
        if (content) content.classList.add('active');
        const TABS = ['visual', 'texto', 'avanzado', 'atajos'];
        const idx = TABS.indexOf(name);
        const tabs = document.querySelectorAll('.a11y-panel-tab');
        if (tabs[idx]) tabs[idx].classList.add('active');
    }

    function setTheme(t) {
        const THEMES = ['default', 'dim', 'light', 'sepia', 'contrast', 'dalton'];
        THEMES.forEach(th => document.body.classList.remove('theme-' + th));
        if (t !== 'default') document.body.classList.add('theme-' + t);
        state.theme = t;
        document.querySelectorAll('.a11y-theme-chip').forEach(c =>
            c.classList.toggle('active', c.dataset.t === t)
        );
        save('theme', t);
        toast('Tema: ' + t);
    }

    function setFilter(f) {
        document.body.classList.remove('filter-invert', 'filter-grayscale', 'low-saturation');
        if (f === 'invert') document.body.classList.add('filter-invert');
        if (f === 'grayscale') document.body.classList.add('filter-grayscale');
        if (f === 'low-saturation') document.body.classList.add('low-saturation');
        state.filter = f;
        ['none', 'invert', 'grayscale', 'low-sat'].forEach(x => {
            const el = document.getElementById('a11y-filter-' + x);
            if (el) el.classList.remove('active');
        });
        const idMap = { 'none': 'none', 'invert': 'invert', 'grayscale': 'grayscale', 'low-saturation': 'low-sat' };
        const btn = document.getElementById('a11y-filter-' + (idMap[f] || f));
        if (btn) btn.classList.add('active');
        save('filter', f);
    }

    function setBrightness(v) {
        v = Math.round(v);
        const wrapper = document.querySelector('.a11y-content-wrapper');
        if (wrapper) wrapper.style.filter = 'brightness(' + v + '%)';
        const val = document.getElementById('a11y-brightness-val');
        if (val) val.textContent = v + '%';
        state.brightness = v;
        save('brightness', v);
    }

    function setFontSize(v) {
        v = Math.round(v);
        document.querySelectorAll('.a11y-target').forEach(el => {
            el.style.fontSize = v + '%';
        });
        const val = document.getElementById('a11y-font-val');
        if (val) val.textContent = v + '%';
        state.fontSize = v;
        save('fontSize', v);
    }

    function setFont(f) {
        ['sans', 'serif', 'mono', 'dyslexia', 'humanist'].forEach(x => {
            document.body.classList.remove('font-' + x);
            const btn = document.getElementById('a11y-font-' + x);
            if (btn) btn.classList.remove('active');
        });
        document.body.classList.add('font-' + f);
        const active = document.getElementById('a11y-font-' + f);
        if (active) active.classList.add('active');
        state.font = f;
        save('font', f);
        toast('Fuente: ' + f);
    }

    function setSpacing(s) {
        ['compact', 'normal', 'wide', 'max'].forEach(x => {
            document.body.classList.remove('spacing-' + x);
            const btn = document.getElementById('a11y-spacing-' + x);
            if (btn) btn.classList.remove('active');
        });
        document.body.classList.add('spacing-' + s);
        const active = document.getElementById('a11y-spacing-' + s);
        if (active) active.classList.add('active');
        state.spacing = s;
        save('spacing', s);
    }

    function setWidth(v) {
        v = Math.round(v / 20) * 20;
        const wrapper = document.querySelector('.a11y-content-wrapper');
        if (wrapper) wrapper.style.maxWidth = v + 'px';
        const val = document.getElementById('a11y-width-val');
        if (val) val.textContent = v + 'px';
        state.width = v;
        save('width', v);
    }

    function toggleFeature(cls, on) {
        document.body.classList.toggle(cls, on);
        state.features[cls] = on;
        save('feat_' + cls, on);
        toast((on ? '✓ ' : '✕ ') + cls.replace(/-/g, ' '));
    }

    function toggleReading(on) {
        if (on) {
            setTheme('sepia');
            setFont('serif');
            setSpacing('wide');
            setFontSize(110);
            const slider = document.getElementById('a11y-font-slider');
            const val = document.getElementById('a11y-font-val');
            if (slider) slider.value = 110;
            if (val) val.textContent = '110%';
        }
        save('reading', on);
        toast(on ? 'Modo lectura activado' : 'Modo lectura desactivado');
    }

    function resetAll() {
        localStorage.clear();
        document.body.className = '';
        setTheme('default');
        setFont('sans');
        setSpacing('normal');
        setFilter('none');

        const fontSlider = document.getElementById('a11y-font-slider');
        const fontVal = document.getElementById('a11y-font-val');
        const brightnessSlider = document.getElementById('a11y-brightness-slider');
        const brightnessVal = document.getElementById('a11y-brightness-val');
        const widthSlider = document.getElementById('a11y-width-slider');
        const widthVal = document.getElementById('a11y-width-val');

        if (fontSlider) fontSlider.value = 100;
        if (fontVal) fontVal.textContent = '100%';
        if (brightnessSlider) brightnessSlider.value = 100;
        if (brightnessVal) brightnessVal.textContent = '100%';
        if (widthSlider) widthSlider.value = 860;
        if (widthVal) widthVal.textContent = '860px';

        document.querySelectorAll('.a11y-target').forEach(el => el.style.cssText = '');
        const wrapper = document.querySelector('.a11y-content-wrapper');
        if (wrapper) { wrapper.style.filter = '';
            wrapper.style.maxWidth = ''; }

        ['tog-cursor', 'tog-focus', 'tog-links', 'tog-motion', 'tog-reading'].forEach(id => {
            const el = document.getElementById('a11y-' + id);
            if (el) el.checked = false;
        });
        toast('Todo restablecido');
    }

    function loadSettings() {
        const t = load('theme', 'default');
        const fi = load('filter', 'none');
        const fo = load('font', 'sans');
        const sp = load('spacing', 'normal');
        const fs = load('fontSize', 100);
        const br = load('brightness', 100);
        const wd = load('width', 860);

        setTheme(t);
        setFilter(fi);
        setFont(fo);
        setSpacing(sp);
        setFontSize(fs);
        setBrightness(br);
        setWidth(wd);

        const fontSlider = document.getElementById('a11y-font-slider');
        const fontVal = document.getElementById('a11y-font-val');
        const brightnessSlider = document.getElementById('a11y-brightness-slider');
        const brightnessVal = document.getElementById('a11y-brightness-val');
        const widthSlider = document.getElementById('a11y-width-slider');
        const widthVal = document.getElementById('a11y-width-val');

        if (fontSlider) fontSlider.value = fs;
        if (fontVal) fontVal.textContent = Math.round(fs) + '%';
        if (brightnessSlider) brightnessSlider.value = br;
        if (brightnessVal) brightnessVal.textContent = Math.round(br) + '%';
        if (widthSlider) widthSlider.value = wd;
        if (widthVal) widthVal.textContent = Math.round(wd / 20) * 20 + 'px';

        const togMap = {
            'big-cursor': 'tog-cursor',
            'show-focus': 'tog-focus',
            'highlight-links': 'tog-links',
            'no-motion': 'tog-motion'
        };

        Object.keys(state.features).forEach(cls => {
            const on = load('feat_' + cls, false);
            if (on) { document.body.classList.add(cls);
                state.features[cls] = true; }
            const el = document.getElementById('a11y-' + togMap[cls]);
            if (el) el.checked = on;
        });
    }

    document.addEventListener('keydown', function(e) {
        if (!e.altKey) return;
        switch (e.key) {
            case 'a':
            case 'A':
                e.preventDefault();
                togglePanel();
                break;
            case '+':
            case '=':
                e.preventDefault(); {
                    const v = Math.min(160, state.fontSize + 10);
                    setFontSize(v);
                    const s = document.getElementById('a11y-font-slider');
                    if (s) s.value = v;
                }
                break;
            case '-':
                e.preventDefault(); {
                    const v = Math.max(80, state.fontSize - 10);
                    setFontSize(v);
                    const s = document.getElementById('a11y-font-slider');
                    if (s) s.value = v;
                }
                break;
            case 't':
            case 'T':
                e.preventDefault();
                state.lightTheme = !state.lightTheme;
                setTheme(state.lightTheme ? 'light' : 'default');
                break;
            case 'c':
            case 'C':
                e.preventDefault();
                setTheme('contrast');
                break;
            case 'r':
            case 'R':
                e.preventDefault();
                resetAll();
                break;
            case 'ArrowRight':
                e.preventDefault(); {
                    const TABS = ['visual', 'texto', 'avanzado', 'atajos'];
                    const i = (TABS.indexOf(state.activeTab) + 1) % TABS.length;
                    switchTab(TABS[i]);
                }
                break;
        }
    });

    document.addEventListener('click', function(e) {
        const panel = document.getElementById('a11y-panel');
        const btn = document.getElementById('a11y-btn');
        if (panel && btn && !panel.contains(e.target) && !btn.contains(e.target)) {
            closePanel();
        }
    });

    window.A11y = {
        togglePanel,
        closePanel,
        switchTab,
        setTheme,
        setFilter,
        setBrightness,
        setFontSize,
        setFont,
        setSpacing,
        setWidth,
        toggleFeature,
        toggleReading,
        resetAll
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadSettings);
    } else {
        loadSettings();
    }
})();