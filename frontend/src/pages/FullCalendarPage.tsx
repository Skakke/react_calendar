import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import type { EventContentArg } from "@fullcalendar/core";

const events = [
  { title: "Meeting", start: new Date() }
];

export default function Calendar() {
  return (
    <div
      style={{
        padding: 20,
        maxWidth: 1400,
        margin: "0 auto"
      }}
    >
      <h1>Calendar</h1>

      <FullCalendar
        plugins={[dayGridPlugin]}
        initialView="dayGridMonth"
        aspectRatio={1.8}
        expandRows={true}
        weekends={false}
        events={events}
        eventContent={renderEventContent}
      />
    </div>
  );
}

// Typed render function (TypeScript-friendly)
function renderEventContent(eventInfo: EventContentArg) {
  return (
    <>
      <b>{eventInfo.timeText}</b>{" "}
      <i>{eventInfo.event.title}</i>
    </>
  );
}
