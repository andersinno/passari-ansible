from jinja2 import contextfilter


@contextfilter
def eval_hostname(context, host):
    if context["inventory_hostname"] == host:
        return "127.0.0.1"
    else:
        return host


class FilterModule(object):
    def filters(self):
        return {
            "eval_hostname": eval_hostname
        }
