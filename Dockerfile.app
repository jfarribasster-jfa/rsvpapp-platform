FROM python:3.7
WORKDIR /app
COPY app /app
RUN chmod -x /app/*py && \
    chmod +x /app/start.sh && \
    chmod +x /app/testing.sh && \
    mkdir /app/.pytest_cache && \
    chmod 777 /app/.pytest_cache && \
    groupadd -r uwsgi && useradd -r -g uwsgi uwsgi && \
    pip install --upgrade pip && \
    pip3 install -r requirements.txt
ENV LINK http://www.meetup.com/cloudyuga/
ENV TEXT1 CloudYuga
ENV TEXT2 Garage RSVP!
ENV LOGO https://raw.githubusercontent.com/cloudyuga/rsvpapp/master/static/cloudyuga.png
ENV COMPANY CloudYuga Technology Pvt. Ltd.
EXPOSE 5000
USER uwsgi
#CMD ["/app/start.sh"]
CMD ["sh", "-c", "exec uwsgi --http 0.0.0.0:5000 --wsgi-file /app/rsvp.py --callable app --stats 0.0.0.0:5001"]

