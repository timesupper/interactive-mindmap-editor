(function (global) {
  'use strict';

  function finite(value, fallback) {
    return Number.isFinite(Number(value)) ? Number(value) : fallback;
  }

  function clone(value) {
    return value == null ? value : JSON.parse(JSON.stringify(value));
  }

  function walk(node, fn, depth) {
    if (!node) return;
    fn(node, depth || 0);
    (Array.isArray(node.children) ? node.children : []).forEach(function (child) {
      walk(child, fn, (depth || 0) + 1);
    });
  }

  function markdownLabel(node) {
    var title = String(node.title || '未命名节点').replace(/\s+/g, ' ').trim();
    var sub = String(node.sub || '').replace(/\s+/g, ' ').trim();
    return sub ? title + '：' + sub : title;
  }

  function toMarkdown(data) {
    var root = data || { title: '思维导图', children: [] };
    var lines = ['# ' + markdownLabel(root)];
    function emit(children, depth) {
      (Array.isArray(children) ? children : []).forEach(function (node) {
        lines.push('  '.repeat(depth) + '- ' + markdownLabel(node));
        emit(node.children, depth + 1);
      });
    }
    emit(root.children, 0);
    return lines.join('\n') + '\n';
  }

  function injectAssets(assets) {
    if (global.markmap && global.markmap.Markmap && global.markmap.Transformer && global.d3) {
      return Promise.resolve();
    }
    if (!assets) return Promise.reject(new Error('Markmap assets are missing.'));
    var decode = function (value) {
      var binary = global.atob(value);
      var bytes = new Uint8Array(binary.length);
      for (var i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
      return new TextDecoder('utf-8').decode(bytes);
    };
    var order = assets.order || Object.keys(assets).filter(function (key) { return key !== 'order'; });
    return order.reduce(function (promise, name) {
      return promise.then(function () {
        if (!assets[name]) return;
        var script = document.createElement('script');
        script.textContent = decode(assets[name]);
        document.head.appendChild(script);
      });
    }, Promise.resolve());
  }

  function Preview(options) {
    options = options || {};
    this.dialog = document.querySelector(options.dialog || '.imm-markmap-dialog');
    this.canvas = document.querySelector(options.canvas || '.imm-markmap-canvas');
    this.assets = options.assets || global.__INTERACTIVE_MINDMAP_MARKMAP_LIBS__;
    this.data = null;
    this.instance = null;
    this.expandLevel = 3;
    this.maxLevel = 3;
    this.renderToken = 0;
    this.fitTimer = null;
    this.onSelect = options.onSelect || function () {};
    this.onEdit = options.onEdit || function () {};
    this.onContextMenu = options.onContextMenu || function () {};
    this.storageKey = options.storageKey || 'interactive-mindmap-editor:markmap-state';
    try {
      var saved = JSON.parse(global.localStorage.getItem(this.storageKey) || '{}');
      this.expandLevel = Math.max(1, finite(saved.expandLevel, this.expandLevel));
    } catch (error) {}
  }

  Preview.prototype.open = function (data) {
    this.data = clone(data);
    if (this.dialog) this.dialog.classList.add('is-open');
    this.saveState(true);
    return this.refresh();
  };

  Preview.prototype.close = function () {
    this.dispose();
    if (this.dialog) this.dialog.classList.remove('is-open');
    this.saveState(false);
  };

  Preview.prototype.refresh = function () {
    var self = this;
    if (!this.data || !this.canvas) return Promise.resolve();
    this.dispose();
    return injectAssets(this.assets).then(function () {
      return self.renderMarkmap();
    }).catch(function (error) {
      self.renderFallback(error.message);
    });
  };

  Preview.prototype.renderMarkmap = function () {
    var self = this;
    var transformer = new global.markmap.Transformer();
    var transformed = transformer.transform(toMarkdown(this.data));
    var root = clone(transformed.root);
    this.maxLevel = Math.max(1, finite(getDepth(root), 1));
    this.expandLevel = Math.max(1, Math.min(this.expandLevel, this.maxLevel));
    applyExpandLevel(root, this.expandLevel);
    this.canvas.innerHTML = '<svg class="imm-markmap-svg"></svg>';
    var svg = this.canvas.querySelector('svg');
    var rect = this.canvas.getBoundingClientRect();
    var width = finite(rect.width || this.canvas.clientWidth, 1);
    var height = finite(rect.height || this.canvas.clientHeight, 1);
    svg.setAttribute('width', String(Math.max(1, Math.round(width))));
    svg.setAttribute('height', String(Math.max(1, Math.round(height))));
    var token = ++this.renderToken;
    requestAnimationFrame(function () {
      if (token !== self.renderToken || !self.dialog.classList.contains('is-open')) return;
      try {
        self.instance = global.markmap.Markmap.create(svg, {
          autoFit: true,
          duration: 300,
          maxWidth: 320,
          spacingVertical: 8,
          spacingHorizontal: 80,
          initialExpandLevel: self.expandLevel
        }, root);
        self.bindCanvas();
        self.fit();
      } catch (error) {
        self.renderFallback(error.message);
      }
    });
  };

  Preview.prototype.renderFallback = function (reason) {
    var self = this;
    this.dispose(false);
    this.canvas.classList.add('imm-markmap-fallback');
    this.canvas.innerHTML = '<p>Markmap 引擎不可用，已切换到本地预览。</p><ul>' + buildFallback(this.data, 0, this) + '</ul>';
    this.bindCanvas();
    if (reason) this.canvas.title = reason;
    self.fit();
  };

  Preview.prototype.bindCanvas = function () {
    var self = this;
    if (this._bound) return;
    this._bound = true;
    this.canvas.addEventListener('click', function (event) {
      var target = event.target.closest('[data-mm-id]');
      self.onSelect(target ? target.dataset.mmId : self.findIdFromEvent(event), event);
    });
    this.canvas.addEventListener('dblclick', function (event) {
      var target = event.target.closest('[data-mm-id]');
      self.onEdit(target ? target.dataset.mmId : self.findIdFromEvent(event), event);
    });
    this.canvas.addEventListener('contextmenu', function (event) {
      var target = event.target.closest('[data-mm-id]');
      var id = target ? target.dataset.mmId : self.findIdFromEvent(event);
      if (id) self.onContextMenu(id, event);
    });
  };

  Preview.prototype.findIdFromEvent = function (event) {
    var text = String(event.target && event.target.textContent || '').replace(/\s+/g, ' ').trim();
    var found = null;
    if (!text || !this.data) return null;
    walk(this.data, function (node) {
      if (!found && (text === markdownLabel(node) || text.indexOf(markdownLabel(node)) !== -1)) found = node.id;
    });
    return found;
  };

  Preview.prototype.fit = function () {
    if (this.instance && this.instance.fit) this.instance.fit();
  };

  Preview.prototype.setExpandLevel = function (level) {
    this.expandLevel = Math.max(1, Math.min(finite(level, 1), this.maxLevel));
    this.saveState(true);
    return this.refresh();
  };

  Preview.prototype.saveState = function (open) {
    try {
      global.localStorage.setItem(this.storageKey, JSON.stringify({
        open: Boolean(open),
        expandLevel: this.expandLevel
      }));
    } catch (error) {}
  };

  Preview.prototype.dispose = function (clear) {
    this.renderToken += 1;
    if (this.fitTimer) clearTimeout(this.fitTimer);
    this.fitTimer = null;
    if (this.instance) {
      try { this.instance.destroy && this.instance.destroy(); } catch (error) {}
    }
    this.instance = null;
    if (clear !== false && this.canvas) {
      this.canvas.classList.remove('imm-markmap-fallback');
      this.canvas.innerHTML = '';
    }
  };

  function getDepth(node) {
    var deepest = 0;
    walk(node, function (_, depth) { deepest = Math.max(deepest, depth); });
    return deepest;
  }

  function applyExpandLevel(node, level, depth) {
    depth = depth || 0;
    var children = Array.isArray(node.children) ? node.children : [];
    node.children = children;
    node.payload = node.payload || {};
    node.payload.fold = children.length > 0 && depth >= level;
    children.forEach(function (child) { applyExpandLevel(child, level, depth + 1); });
  }

  function buildFallback(node, depth, preview) {
    var children = Array.isArray(node.children) ? node.children : [];
    var id = String(node.id || node.v || node.title || 'node-' + depth);
    var html = '<div class="imm-mm-node" data-mm-id="' + escapeHtml(id) + '">' + escapeHtml(markdownLabel(node)) + '</div>';
    if (!children.length) return '<li>' + html + '</li>';
    var collapsed = depth >= preview.expandLevel;
    return '<li>' + html + (collapsed ? '' : '<ul>' + children.map(function (child) { return buildFallback(child, depth + 1, preview); }).join('') + '</ul>') + '</li>';
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (char) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char];
    });
  }

  global.InteractiveMindmapMarkmap = { Preview: Preview, toMarkdown: toMarkdown };
}(window));
