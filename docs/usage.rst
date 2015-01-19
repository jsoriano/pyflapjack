=====
Usage
=====

Events example::

    from pyflapjack.event import FlapjackReceiver, FlapjackEvent
    receiver = FlapjackReceiver()  # connect to redis@localhost:6379/0
    event = FlapjackEvent(
        entity='user-1324564', check='heart-rate', type_='service',
        state='ok'
    )
    receiver.send_events(event)

Jsonapi example::

    from pyflapjack.jsonapi import FlapjackAPI, Contact
    api = FlapjackAPI()  # connect to flapjack api at http://localhost:3081
    contact = Contact(
        id='1', first_name='Harry', last_name='L', email='blurrcat@gmail.com',
        timezone='Asia/Singapore'
    )

    # create a contact
    api.create(contact)

    # query contacts
    contacts = api.query(Contact)
    assert contacts[0].id == contact.id

    # update email of a contact
    email_patch = contact.attr_patch('email', 'blurrcat2@gmail.com')
    api.patch([email_patch], contact.id)
    contact = api.query(Contact, contact.id)[0]
    assert contact.email == 'blurrcat2@gmail.com'

    # delete the contact
    api.delete(Contact, contact.id)

