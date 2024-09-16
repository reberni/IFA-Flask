
def productModel(dbmodel):
    class Products(dbmodel):
        def something (self):
            return self
    return Products