from exts import db


"""" This is my database classes. They reprsent db tables """

class services(db.Enum):
    CustomStrategyDevelopment = "Custom Strategy Development"
    AlgorithmicTrading = "Algorithmic Trading"
    Multi-PlatformIntegration = "Multi-Platform Integration"
    RiskManagementSolutions = "Risk Management Solutions"
    StrategyOptimization = "Strategy Optimization"
    PerformanceAnalytics = "Performance Analytics" 


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    date_time = db.Column(db.String, nullable=False)
    # timezone = db.Column(db.String, nullable=False)
    service = db.Column(db.String, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    meet_link = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f" A Booking for {self.f_name} {self.l_name} on {self.date_time} for {self.service} "; 
    
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

    