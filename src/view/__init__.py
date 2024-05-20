from uix.core.element import Element

class DigitArea(Element):
    def __init__(self, id: str = None, placeholder: str = None, required: bool = False, max_length: int = None):
        super().__init__(id=id)
        self.tag = "textarea"
        self.attrs["placeholder"] = placeholder
        self.attrs["pattern"] = "[01]*"  # Regular expression to allow only 0 or 1
        self.classes.append("digit-area")
        if required:
            self.attrs["required"] = "required"
        if max_length is not None:
            self.attrs["maxlength"] = str(max_length)  # Restrict the maximum length

    def disabled(self):
        self.attrs["disabled"] = "disabled"
        return self