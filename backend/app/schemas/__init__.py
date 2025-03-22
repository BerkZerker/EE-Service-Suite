from app.schemas.user import User, UserCreate, UserUpdate
from app.schemas.customer import Customer, CustomerCreate, CustomerUpdate, CustomerWithBikes
from app.schemas.bike import Bike, BikeCreate, BikeUpdate, BikeWithTickets
from app.schemas.ticket import Ticket, TicketCreate, TicketUpdate, TicketWithDetails
from app.schemas.ticket_update import TicketUpdate as TicketUpdateSchema
from app.schemas.part import Part, PartCreate, PartUpdate
from app.schemas.ticket_part import TicketPart, TicketPartCreate, TicketPartUpdate
from app.schemas.service import Service, ServiceCreate, ServiceUpdate