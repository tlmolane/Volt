(function ($) {

Drupal.behaviors.commentNotify = {
  attach: function (context) {
    $('#edit-notify', context)
      .bind('change', function() {
        $('#edit-notify-type', context)
          [this.checked ? 'show' : 'hide']()
          .find('input[type=checkbox]:checked').attr('checked', 'checked');
      })
      .trigger('change');
  }
}

})(jQuery);
;
(function($) {
  Drupal.behaviors.panopolyImagesModule = {
    attach: function (context, settings) {
      var captions = $('.caption', context).has('img');
      $(captions).once('panopoly-images').imagesLoaded(function () {
        panopolyImagesResizeCaptionBox(captions);
      });

      function panopolyImagesResizeCaptionBox(captions) {
        captions.each(function() {
          var imageSet = $('img', this),
              imgBoxWidth = getImgWidth(imageSet),
              wrapperBoxWidth =
                  getWrapperSpacing($('.caption-inner', this))
                + getWrapperSpacing($('.caption-width-container', this)),
              totalWidth = imgBoxWidth + wrapperBoxWidth;
          $(this).width(totalWidth);
        });
      }

      // Get width of image plus margins, borders and padding
      function getImgWidth(imageSet) {
        var imgWidth = 0,
            imgBoxExtra = 0,
            testWidth = 0;
        var attrWidth;

        // We shouldn't have more than one image in a caption, but it would be
        // possible, so we make sure we have the widest one
        for (var i = 0; i < imageSet.length; i++) {
          // If we have a hardcoded width attribute from manual resizing in
          // TinMCE, use that. If not, use the image naturalWidth. We can't
          // reliably use width() for responsive images.
          attrWidth = $(imageSet[i]).attr("width");
          if (typeof attrWidth !== 'undefined') {
            // attr() returns a string. Must convert to int for math to work.
            testWidth = parseInt(attrWidth, 10);
          }
          else {
            testWidth = imageSet[i].naturalWidth;
          }
          if (testWidth > imgWidth) {
            imgWidth = testWidth;
            imgBoxExtra = getWrapperSpacing(imageSet[i])
          }
        }
        return imgWidth + imgBoxExtra;
      }

      // We want the total of margin, border and padding on the element
      function getWrapperSpacing(el) {
        var spacing = ['margin-left', 'border-left', 'padding-left', 'padding-right', 'border-right', 'margin-right'],
            totalPx = 0,
            spacePx = 0,
            spaceRaw = '';
        for (var i = 0; i < spacing.length; i++) {
          spaceRaw = $(el).css(spacing[i]);

          // Themers might add padding, borders or margin defined in ems, but we can't
          // add that to pixel dimensions returned by naturalWidth, so we just throw
          // away anything but pixels. Themers have to deal with that.
          if(spaceRaw && spaceRaw.substr(spaceRaw.length - 2) == 'px') {
            spacePx = parseInt(spaceRaw, 10);
            totalPx += ($.isNumeric(spacePx)) ? spacePx : 0;
          }
        }
        return totalPx;
      }
    }
  }
})(jQuery);
;
(function ($) {

 /**
   * UI Improvements for the Content Editing Form
   */
 Drupal.behaviors.panopolyAdmin = {
   attach: function (context, settings) {
     // Make the permalink field full width.
     var width = $('#node-edit #edit-title').width() - $('#node-edit .form-item-path-alias label').width() - $('#node-edit .form-item-path-alias .field-prefix').width() - 10;
     $('#node-edit .form-item-path-alias input').css('width', width);

     // Hide the body label in Javascript if requested, which allows the summary
     // Javacript to continue working.
     $('#node-edit .panopoly-admin-hide-body-label .form-item-body-und-0-value label', context)
      .once('panopoly-admin-hide-body-label')
      .wrapInner('<span class="element-invisible"></span>')
      .css('text-align', 'right');

     if ($('#node-edit .form-item-field-featured-image-und-0-alt label')) {
       $('#node-edit .form-item-field-featured-image-und-0-alt label').html('Alt Text');
     }
   }
 }

 /**
   * Automatically Upload Files/Images Attached
   */
 Drupal.behaviors.panopolyAutoUpload = {
    attach: function (context, settings) {
      $('#node-edit input#edit-field-featured-image-und-0-upload').next('input[type="submit"]').hide();
      $('form', context).delegate('#node-edit input#edit-field-featured-image-und-0-upload', 'change', function() {  
        $(this).next('input[type="submit"]').mousedown();
      }); 
    }
  };

  /**
   * Automatically fill in a menu link title, if possible.
   *
   * NOTE: This behavior is a copy and paste from the Core Menu module's menu.js
   * script. It has been adapted to update proper targeting. This brings back
   * the core functionality.
   */
  Drupal.behaviors.panopolyLinkAutomaticTitle = {
    attach: function (context) {
      $('.pane-node-form-menu', context).each(function () {
        // Try to find menu settings widget elements as well as a 'title' field in
        // the form, but play nicely with user permissions and form alterations.
        var $checkbox = $('.form-item-menu-enabled input', this);
        var $link_title = $('.form-item-menu-link-title input', context);
        var $title = $(this).closest('form').find('.form-item-title input');
        // Bail out if we do not have all required fields.
        if (!($checkbox.length && $link_title.length && $title.length)) {
          return;
        }
        // If there is a link title already, mark it as overridden. The user expects
        // that toggling the checkbox twice will take over the node's title.
        if ($checkbox.is(':checked') && $link_title.val().length) {
          $link_title.data('menuLinkAutomaticTitleOveridden', true);
        }
        // Whenever the value is changed manually, disable this behavior.
        $link_title.keyup(function () {
          $link_title.data('menuLinkAutomaticTitleOveridden', true);
        });
        // Global trigger on checkbox (do not fill-in a value when disabled).
        $checkbox.change(function () {
          if ($checkbox.is(':checked')) {
            if (!$link_title.data('menuLinkAutomaticTitleOveridden')) {
              $link_title.val($title.val());
            }
          }
          else {
            $link_title.val('');
            $link_title.removeData('menuLinkAutomaticTitleOveridden');
          }
          $checkbox.closest('fieldset.vertical-tabs-pane').trigger('summaryUpdated');
          $checkbox.trigger('formUpdated');
        });
        // Take over any title change.
        $title.keyup(function () {
          if (!$link_title.data('menuLinkAutomaticTitleOveridden') && $checkbox.is(':checked')) {
            $link_title.val($title.val());
            $link_title.val($title.val()).trigger('formUpdated');
          }
        });
      });
    }
  };

})(jQuery);
;
(function ($) {
  Drupal.behaviors.panopolyMagic = {
    attach: function (context, settings) {
      /**
       * Title Hax for Panopoly
       *
       * Replaces the markup of a node title pane with
       * the h1.title page element
       */
      if ($.trim($('.pane-node-title .pane-content').html()) == $.trim($('h1.title').html())) {
        $('.pane-node-title .pane-content').html('');
        $('h1.title').hide().clone().prependTo('.pane-node-title .pane-content');
        $('.pane-node-title h1.title').show();
      }
    }
  };
})(jQuery);

(function ($) {
  // Used to only update preview after changes stop for a second.
  var timer;

  // Used to make sure we don't wrap Drupal.wysiwygAttach() more than once.
  var wrappedWysiwygAttach = false;

  // Used to make sure we don't wrap insertLink() on the Linkit field helper
  // more than once.
  var wrappedLinkitField = false;

  // Triggers the CTools autosubmit on the given form. If timeout is passed,
  // it'll set a timeout to do the actual submit rather than calling it directly
  // and return the timer handle.
  function triggerSubmit(form, timeout) {
    var $form = $(form),
        preview_widget = $('#panopoly-form-widget-preview'),
        submit;
    if (!preview_widget.hasClass('panopoly-magic-loading')) {
      preview_widget.addClass('panopoly-magic-loading');
      submit = function () {
        if (document.contains(form)) {
          $form.find('.ctools-auto-submit-click').click();
        }
      };
      if (typeof timeout === 'number') {
        return setTimeout(submit, timeout);
      }
      else {
        submit();
      }
    }
  }

  // Used to cancel a submit. It'll clear the timer and the class marking the
  // loading operation.
  function cancelSubmit(form, timer) {
    var $form = $(form),
        preview_widget = $('#panopoly-form-widget-preview');
    preview_widget.removeClass('panopoly-magic-loading');
    clearTimeout(timer);
  }

  function onWysiwygChangeFactory(editorId) {
    return function () {
      var textarea = $('#' + editorId),
          form = textarea.get(0).form;

      if (textarea.hasClass('panopoly-textarea-autosubmit')) {
        // Wait a second and then submit.
        cancelSubmit(form, timer); 
        timer = triggerSubmit(form, 1000);
      }
    };
  }

  // A function to run before Drupal.wysiwyg.editor.attach.tinymce() with the
  // same arguments.
  function wysiwygTinymceBeforeAttach(context, params, settings) {
    var onWysiwygChange = onWysiwygChangeFactory(params.field);
    settings['setup'] = function (editor) {
      editor.onChange.add(onWysiwygChange);
      editor.onKeyUp.add(onWysiwygChange);
    };
  }

  // A function to run before Drupal.wysiwyg.editor.attach.markitup() with the
  // same arguments.
  function wysiwygMarkitupBeforeAttach(context, params, settings) {
    var onWysiwygChange = onWysiwygChangeFactory(params.field);
    $.each(['afterInsert', 'onEnter'], function (index, funcName) {
      settings[funcName] = onWysiwygChange;
    });
  }

  // Used to wrap a function with a beforeFunc (we use it for wrapping
  // Drupal.wysiwygAttach()).
  function wrapFunctionBefore(parent, name, beforeFunc) {
    var originalFunc = parent[name];
    parent[name] = function () {
      beforeFunc.apply(this, arguments);
      return originalFunc.apply(this, arguments);
    };
  }

  // Used to wrap a function with an afterFunc (we use it for wrapping
  // insertLink() on the Linkit field helper);
  function wrapFunctionAfter(parent, name, afterFunc) {
    var originalFunc = parent[name];
    parent[name] = function () {
      var retval = originalFunc.apply(this, arguments);
      afterFunc.apply(this, arguments);
      return retval;
    };
  }

  /**
   * Improves the Auto Submit Experience for CTools Modals
   */
  Drupal.behaviors.panopolyMagicAutosubmit = {
    attach: function (context, settings) {
      // Move focus to preview after it's shown.
      $('body').once(function () {
        if (typeof Drupal.CTools !== 'undefined' && typeof Drupal.CTools.Modal !== 'undefined' && typeof Drupal.CTools.Modal.modal_display) {
          var modal_display = Drupal.CTools.Modal.modal_display;
          Drupal.CTools.Modal.modal_display = function (ajax, response, status) {
            var url = ajax.url,
                params = {},
                widget_name;

            // Do the parent operation.
            modal_display(ajax, response, status);

            // Parse the GET arguments.
            url.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(str, key, value) {
              params[key] = value;
            })
            if (params['panopoly_magic_preview'] == 'manual') {
              widget_name = decodeURIComponent(params['preview_panes']).split(',').pop();
              widget_name.replace(':', '-');
              widget_name.replace(/[^a-zA-Z0-9_]/g, '');
              // Need to defer until current set of behaviors is done, because Panels
              // will move the focus to the first widget by default.
              setTimeout(function () {
                $('#modal-content .panopoly-magic-preview-' + widget_name + ' :focusable:first').focus();
              }, 0);
            }
            else if (params['panopoly_magic_preview'] == 'single') {
              // Ditto.
              setTimeout(function () {
                $('#modal-content .panopoly-magic-preview :focusable:first').focus();
              }, 0);
            }
          };
        }
      });

      // Replaces click with mousedown for submit so both normal and ajax work.
      $('.ctools-auto-submit-click', context)
      .click(function(event) {
        if ($(this).hasClass('ajax-processed')) {
          event.stopImmediatePropagation();
          $(this).trigger('mousedown');
          return false;
        }
      });

      // e.keyCode: key
      var discardKeyCode = [
        16, // shift
        17, // ctrl
        18, // alt
        20, // caps lock
        33, // page up
        34, // page down
        35, // end
        36, // home
        37, // left arrow
        38, // up arrow
        39, // right arrow
        40, // down arrow
         9, // tab
        13, // enter
        27  // esc
      ];

      // Special handling for link field widgets. This ensures content which is ahah'd in still properly autosubmits.
      $('.field-widget-link-field input:text', context).addClass('panopoly-textfield-autosubmit').addClass('ctools-auto-submit-exclude');

      // Handle text fields and textareas.
      $('.panopoly-textfield-autosubmit, .panopoly-textarea-autosubmit', context)
      .once('ctools-auto-submit')
      .bind('keyup blur', function (e) {
        var $element;
        $element = $('.panopoly-magic-preview .pane-title', context);

        cancelSubmit(e.target.form, timer);

        // Filter out discarded keys.
        if (e.type !== 'blur' && $.inArray(e.keyCode, discardKeyCode) > 0) {
          return;
        }

        // Set a timer to submit the form a second after the last activity.
        timer = triggerSubmit(e.target.form, 1000);
      });

      // Handle WYSIWYG fields.
      if (!wrappedWysiwygAttach && typeof Drupal.wysiwyg != 'undefined' && typeof Drupal.wysiwyg.editor.attach.tinymce == 'function' && typeof Drupal.wysiwyg.editor.attach.markitup == 'function') {
        wrapFunctionBefore(Drupal.wysiwyg.editor.attach, 'tinymce', wysiwygTinymceBeforeAttach);
        //wrapFunctionBefore(Drupal.wysiwyg.editor.attach, 'markitup', wysiwygMarkitupBeforeAttach);
        wrappedWysiwygAttach = true;

        // Since the Drupal.behaviors run in a non-deterministic order, we can
        // never be sure that we wrapped Drupal.wysiwygAttach() before it was
        // used! So, we look for already attached editors so we can detach and
        // re-attach them.
        $('.panopoly-textarea-autosubmit', context)
        .once('panopoly-magic-wysiwyg')
        .each(function () {
          var editorId = this.id,
              instance = Drupal.wysiwyg.instances[editorId],
              format = instance ? instance.format : null,
              trigger = instance ? instance.trigger : null;

          if (instance && instance.editor != 'none') {
            params = Drupal.settings.wysiwyg.triggers[trigger];
            if (params) {
              Drupal.wysiwygDetach(context, params[format]);
              Drupal.wysiwygAttach(context, params[format]);
            }
          }
        });
      }
  
      // Handle autocomplete fields.
      $('.panopoly-autocomplete-autosubmit', context)
      .once('ctools-auto-submit')
      .bind('keyup blur', function (e) {
        // Detect when a value is selected via TAB or ENTER.
        if (e.type === 'blur' || e.keyCode === 13) {
          // We defer the submit call so that it happens after autocomplete has
          // had a chance to fill the input with the selected value.
          triggerSubmit(e.target.form, 0);
        }
      });

      // Prevent ctools auto-submit from firing when changing text formats.
      $(':input.filter-list').addClass('ctools-auto-submit-exclude');

      // Handle Linkit fields.
      if (!wrappedLinkitField && typeof Drupal.linkit !== 'undefined') {
        var linkitFieldHelper = Drupal.linkit.getDialogHelper('field');
        if (typeof linkitFieldHelper !== 'undefined') {
          wrapFunctionAfter(linkitFieldHelper, 'insertLink', function (data) {
            var element = document.getElementById(Drupal.settings.linkit.currentInstance.source);
            triggerSubmit(element.form);
          });
          wrappedLinkitField = true;
        }
      }

    }
  }
})(jQuery);
;
(function ($) {

  Drupal.behaviors.PanelsAccordionStyle = {
    attach: function (context, settings) {
      for (region_id in Drupal.settings.accordion) {
        var accordion = Drupal.settings.accordion[region_id];
        if (jQuery('#'+region_id).hasClass("ui-accordion")) {
          jQuery('#'+region_id).accordion("refresh");
        } else {
          jQuery('#'+region_id).accordion(accordion.options);
        }
      }
    }
  };

})(jQuery);
;
/**
 * @file
 * JavaScript integrations between the Caption Filter module and particular
 * WYSIWYG editors. This file also implements Insert module hooks to respond
 * to the insertion of content into a WYSIWYG or textarea.
 */
(function ($) {

$(document).bind('insertIntoActiveEditor', function(event, options) {
  if (options['fields']['title'] && Drupal.settings.captionFilter.widgets[options['widgetType']]) {
    options['content'] = '[caption caption="' + options['fields']['title'].replace(/"/g, '\\"') + '"]' + options['content'] + '[/caption]';
  }
});

Drupal.captionFilter = Drupal.captionFilter || {};

Drupal.captionFilter.toHTML = function(co, editor) {
  return co.replace(/(?:<p>)?\[caption([^\]]*)\]([\s\S]+?)\[\/caption\](?:<\/p>)?[\s\u00a0]*/g, function(a,b,c){
    var id, cls, w, tempClass;

    b = b.replace(/\\?'|\\&#39;|\\&#039;/g, '&#39;').replace(/\\"|\\&quot;/g, '&quot;');
    c = c.replace(/\\&#39;|\\&#039;/g, '&#39;').replace(/\\&quot;/g, '&quot;');
    id = b.match(/id=['"]([^'"]+)/i);
    cls = b.match(/align=['"]([^'"]+)/i);
    ct = b.match(/caption=['"]([^'"]+)/i);
    w = c.match(/width=['"]([0-9]+)/);

    id = ( id && id[1] ) ? id[1] : '';
    cls = ( cls && cls[1] ) ? 'caption-' + cls[1] : '';
    ct = ( ct && ct[1] ) ? ct[1].replace(/\\\\"/,'"') : '';
    w = ( w && w[1] ) ? parseInt(w[1])+'px' : 'auto';

    if (editor == 'tinymce')
      tempClass = (cls == 'caption-center') ? 'mceTemp mceIEcenter' : 'mceTemp';
    else if (editor == 'ckeditor')
      tempClass = (cls == 'caption-center') ? 'mceTemp mceIEcenter' : 'mceTemp';
    else
      tempClass = '';

    if (ct) {
      return '<div class="caption ' + cls + ' ' + tempClass + ' draggable"><div class="caption-width-container" style="width: ' + w + '"><div class="caption-inner">' + c + '<p class="caption-text">' + ct + '</p></div></div></div><br />';
    }
    else {
      return '<div class="caption ' + cls + ' ' + tempClass + ' draggable"><div class="caption-width-container" style="width: ' + w + '"><div class="caption-inner">' + c + '</div></div></div><br />';
    }
  });
};

Drupal.captionFilter.toTag = function(co) {
  return co.replace(/(<div class="caption [^"]*">)\s*<div[^>]+>\s*<div[^>]+>(.+?)<\/div>\s*<\/div>\s*<\/div>\s*/gi, function(match, captionWrapper, contents) {
    var align;
    align = captionWrapper.match(/class=.*?caption-(left|center|right)/i);
    align = (align && align[1]) ? align[1] : '';
    caption = contents.match(/\<p class=\"caption-text\"\>(.*)\<\/p\>/);
    caption_html = (caption && caption[0]) ? caption[0] : '';
    caption = (caption && caption[1]) ? caption[1].replace(/"/g, '\\"') : '';
    contents = contents.replace(caption_html, '');

    return '[caption' + (caption ? (' caption="' + caption + '"') : '') + (align ? (' align="' + align + '"') : '') + ']' + contents + '[/caption]';
  });
};

})(jQuery);
;
