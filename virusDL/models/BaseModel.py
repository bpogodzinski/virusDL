class BaseModel:
    NAME = 'BaseModel'
    
    def get_name(self):
        layers = '-'.join(f"({layer.name.split('_')[0]}-{layer.units})"for layer in self.model.layers)
        return f"{self.NAME}-{layers}"
    
    def get_model(self):
        return self.model