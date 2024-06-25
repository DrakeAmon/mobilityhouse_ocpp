import asyncio
import logging

try:
    import websockets
except ModuleNotFoundError:
    print("This example relies on the 'websockets' package.")
    print("Please install it by running: ")
    print()
    print(" $ pip install websockets")
    import sys

    sys.exit(1)


from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call

from ocpp.v16.datatypes import MeterValue, SampledValue

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    async def send_heartbeat(self, interval):
        request = call.HeartbeatPayload()
        while True:
            await self.call(request)
            await asyncio.sleep(interval)

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charging_station={"model": "Wallbox XYZ", "vendor_name": "anewone"},
            reason="PowerUp",
        )
        response = await self.call(request)

        if response.status == "Accepted":
            print("Connected to central system.")
            await self.send_meter_values()
            await self.send_heartbeat(response.interval)

    async def send_meter_values(self):

        request = call.MeterValuesPayload(
        connector_id=3,
        meter_value=[
            MeterValue(
                timestamp="2017-08-17T07:08:06.186748+00:00",
                sampled_value=[
                    SampledValue(
                        value="10",
                        context="Sample.Periodic",
                        format=None,
                        measurand="Power.Active.Import",
                        phase=None,
                        location=None,
                        unit="W",
                    ),
                    SampledValue(
                        value="50000",
                        context="Sample.Periodic",
                        format=None,
                        measurand="Power.Active.Import",
                        phase="L1",
                        location=None,
                        unit="W",
                    ),
                ],
            ),
            MeterValue(
                timestamp="2017-08-17T07:07:07.186748+00:00",
                sampled_value=[
                    SampledValue(
                        value="10",
                        context="Sample.Periodic",
                        format=None,
                        measurand="Power.Active.Import",
                        phase=None,
                        location=None,
                        unit="W",
                    ),
                    SampledValue(
                        value="50000",
                        context="Sample.Periodic",
                        format=None,
                        measurand="Power.Active.Import",
                        phase="L1",
                        location=None,
                        unit="W",
                    ),
                ],
            ),
        ],
        transaction_id=5,
    )
        response = await self.call(request)
        print("Test erfolgreich")


async def main():
    async with websockets.connect(
        "ws://localhost:9000/CP_1", subprotocols=["ocpp2.0.1"]
    ) as ws:

        charge_point = ChargePoint("CP_1", ws)
        await asyncio.gather(
            charge_point.start(), charge_point.send_boot_notification()
        )


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
