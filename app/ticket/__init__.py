from .routes import TicketList, TicketDetail, MessageList, MessageDetail


def init_app(api):
    api.add_resource(TicketList, '/tickets/')
    api.add_resource(TicketDetail, '/tickets/<int:id>')
    api.add_resource(MessageList, '/messages/')
    api.add_resource(MessageDetail, '/messages/<int:id>')
