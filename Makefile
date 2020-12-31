about:
	@echo "Project tasks"

SP-MUN.zip:
	wget http://www.usp.br/nereus/wp-content/uploads/SP-MUN.zip

35MUE250GC_SIR.shp: SP-MUN.zip
	unzip $^

