TARGET	=	accounting.db
DEPS	=	database.sql \
			populate.sql

all: $(TARGET)

$(TARGET): $(DEPS)
	python3 create_database.py
	cp $(TARGET) ..

clean:
	-rm -rf $(TARGET)
