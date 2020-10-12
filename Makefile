TARGET	=	accounting
DEPS	=	main.py \
			system/database.py \
			system/forms.py \
			system/logger.py \
			system/notebook.py \
			dialogs/select_dialog.py \
			dialogs/text_dialog.py \
			policy/importer.py \
			widgets/form_widgets.py \
			widgets/search_widget.py

all: $(TARGET)

$(TARGET): $(DEPS)
	pyinstaller -F -n accounting main.py

clean:
	-rm -rf *.spec dist/ build/ __pycache__