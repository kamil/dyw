# -*- coding: utf-8 -*-

from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.utils.text import smart_split
register = template.Library()
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

@register.tag(name="render_collection")
def do_render_collection(parser, token):
    """
    {% render_collection objects template_name [context [item_context]] %}
    """
    bits = list(smart_split(token.contents))
    if len(bits) < 3 or len(bits) > 5:
        raise TemplateSyntaxError(_('wrong arguments to render_collection'))
    
    return RenderCollectionNode(*bits[1:])
    
class RenderCollectionNode(template.Node):
    def __init__(self, objects, template_name, context=None, item_context=None):
        self.objects = objects
        self.template = get_template(template_name)
        self.context = context
        self.item_context = item_context
        
    def render(self, context):
        ctx = template.Context(context)
        if self.context:
            ctx.update(self.context)
        
        ctx['item_context'] = self.item_context
        ctx['objects'] = template.resolve_variable(self.objects, context)
        return self.template.render(ctx)
        
@register.tag(name="render_object")
def do_render_object(parser, token):
    """
    {% render_object object template_name [context] %}
    """
    bits = list(smart_split(token.contents))
    if len(bits) not in (3, 4):
        raise TemplateSyntaxError(_('wrong arguments to render_object'))
    
    return RenderObjectNode(*bits[1:])
    
class RenderObjectNode(template.Node):
    def __init__(self, obj, template_name, context=None):
        self.object = obj
        self.template = get_template(template_name)
        self.context = context
        
    def render(self, context):
        ctx = template.Context(context)
        if self.context:
            ctx.update(self.context)
        ctx['object'] = template.resolve_variable(self.object, context)
        return self.template.render(ctx)
        
    
@register.tag(name='render')
def do_render(parser, token):
    """Freestyle render z wszystkim.
    {% render template_name key=value key1=value1 ... %}
    Bajery:
     * jako template_name i values można dać string albo nazwę zmiennej
     * jeśli string w value ma prefix _ (_"dupa") to jest rybką.
     * dziedziczy cały parent context, nadpisuje go podanymi kluczami
     
    """
    bits = list(smart_split(token.contents))
    if len(bits) < 2:
        raise TemplateSyntaxError(_('not enough arguments to render'))
    
    return RenderNode(bits[1:])
    
class RenderNode(template.Node):
    def __init__(self, items):
        self.template = get_template(items.pop(0))
        self.vars = {}
        for item in items:
            lval, _eq, expr = item.partition('=')
            self.vars[lval] = expr
            
    def render(self, context):
        ctx = template.Context(context)
        for name, expr in self.vars.items():
            if expr.startswith('_"') or expr.startswith("_'"):
                expr = _(expr[2:-1])
            else:
                expr = template.resolve_variable(expr, context)
            ctx[name] = expr
        return self.template.render(ctx)
        
