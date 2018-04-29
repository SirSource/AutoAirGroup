from dao.category import CategoryDao


class CategoryHandler:

    def getCategories(self):
        dao = CategoryDao()
        categories = dao.getCategories()
        return categories

    def insertCategoryItem(self, form):
        item = form['category']
        if item == '':
            return False, None, 'invalid_form'
        else:
            return CategoryDao().insertCategoryItem(item), 'category_added'

    def deleteCategoryItem(self, item):
        if self.countCategory(item) > 0:
            return False, None, 'category_in_use'
        else:
            deleted = CategoryDao().deleteCategoryItem(item)
            return True, deleted, 'category_deleted'

    def countCategory(self, item):
        return CategoryDao().countCategory(item)