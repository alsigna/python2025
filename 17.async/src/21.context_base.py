import contextvars

var = contextvars.ContextVar("var", default="default")

print(var.get())  # default

var.set("old-value")
print(var.get())  # old-value

token = var.set("new-value")
print(var.get())  # new_value

var.reset(token)
print(var.get())  # old-value
