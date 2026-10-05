from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .serializers import OrderSerializer
from .services import find_suitable_box


class CreateOrderView(APIView):

    def post(self, request):

        serializer = OrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        order = serializer.save()

        box = find_suitable_box(order)

        if box is None:
            return Response(
                {
                    "order_id": order.id,
                    "recommended_box": None,
                    "message": "No suitable box found."
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "order_id": order.id,
                "recommended_box": {
                    "id": box.id,
                    "name": box.name,
                    "cost": float(box.cost)
                },
                "message": "Suitable box found."
            },
            status=status.HTTP_201_CREATED
        )