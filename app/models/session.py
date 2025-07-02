class Session():

    def __init__(self, idSessao, tipoServico, dataServico, horarioServico, detalhes, cliente):
        self.idSessao= idSessao
        self.tipoServico= tipoServico
        self.dataServico= dataServico
        self.horarioServico= horarioServico
        self.detalhes= detalhes
        self.cliente= cliente
