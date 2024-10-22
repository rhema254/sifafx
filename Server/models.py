from Server.exts import db
import datetime



"""" This is my database classes. They reprsent db tables """

class services(db.Enum):
    CustomStrategyDevelopment = "Custom Strategy Development"
    AlgorithmicTrading = "Algorithmic Trading"
    MultiPlatformIntegration = "Multi-Platform Integration"
    RiskManagementSolutions = "Risk Management Solutions"
    StrategyOptimization = "Strategy Optimization"
    PerformanceAnalytics = "Performance Analytics" 


class Status(db.Enum):
    Scheduled = "Scheduled" 
    CallOngoing = "Call-Ongoing"
    Done = "Done"


class Booking(db.Model):
    """ The data attributes for each booking record """
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(30), nullable=False)
    l_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    timezone = db.Column(db.String(30), nullable=False)
    service = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    meet_link = db.Column(db.String(60), nullable=True, default = 'none')
    status = db.Column(db.String(10), nullable=False, default = Status.Scheduled)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):     
        return f" A Booking for {self.f_name} {self.l_name} in timezone {self.timezone} on {self.date} at {self.time} for {self.service} "; 
    
    #Convenience Methods. 

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save() 

