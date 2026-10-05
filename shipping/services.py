from itertools import permutations


def dimensions_fit(item_dimensions, box_dimensions):
    """
    Check whether an item can fit inside a box in any orientation.
    """

    for dimensions in permutations(item_dimensions):
        if all(
            dimensions[i] <= box_dimensions[i]
            for i in range(3)
        ):
            return True

    return False


def get_orientations(dimensions):
    """
    Return all possible orientations of an item's dimensions.
    """
    return list(permutations(dimensions))


def can_pack_items(items, box):
    """
    Try to pack all items into a box using a simple 3D
    shelf-style packing heuristic.

    Each item is represented as:
        (length, width, height)
    """

    box_dimensions = (
        float(box.internal_length),
        float(box.internal_width),
        float(box.internal_height),
    )

    # Larger items are placed first.
    items = sorted(
        items,
        key=lambda item: item[0] * item[1] * item[2],
        reverse=True,
    )

    # Check every item can theoretically fit in the box.
    for item in items:
        if not dimensions_fit(item, box_dimensions):
            return False

    # Current packing position.
    current_x = 0.0
    current_y = 0.0
    current_z = 0.0

    current_row_width = 0.0
    current_layer_height = 0.0

    for item in items:

        placed = False

        # Try all possible orientations.
        for length, width, height in get_orientations(item):

            # Try placing the item in the current row.
            if (
                current_x + length <= box_dimensions[0]
                and current_y + width <= box_dimensions[1]
                and current_z + height <= box_dimensions[2]
            ):
                current_x += length
                current_row_width = max(
                    current_row_width,
                    width
                )
                current_layer_height = max(
                    current_layer_height,
                    height
                )
                placed = True
                break

        if placed:
            continue

        # Start a new row.
        current_x = 0.0
        current_y += current_row_width
        current_row_width = 0.0

        for length, width, height in get_orientations(item):

            if (
                current_x + length <= box_dimensions[0]
                and current_y + width <= box_dimensions[1]
                and current_z + height <= box_dimensions[2]
            ):
                current_x += length
                current_row_width = max(
                    current_row_width,
                    width
                )
                current_layer_height = max(
                    current_layer_height,
                    height
                )
                placed = True
                break

        if placed:
            continue

        # Start a new layer.
        current_x = 0.0
        current_y = 0.0
        current_z += current_layer_height

        current_row_width = 0.0
        current_layer_height = 0.0

        for length, width, height in get_orientations(item):

            if (
                current_x + length <= box_dimensions[0]
                and current_y + width <= box_dimensions[1]
                and current_z + height <= box_dimensions[2]
            ):
                current_x += length
                current_row_width = max(
                    current_row_width,
                    width
                )
                current_layer_height = max(
                    current_layer_height,
                    height
                )
                placed = True
                break

        if not placed:
            return False

    return True


def calculate_order_requirements(order):
    """
    Calculate total weight and product dimensions
    required for an order.
    """

    total_weight = 0
    items = []

    for order_item in order.items.select_related("product"):
        product = order_item.product

        total_weight += float(product.weight) * order_item.quantity

        for _ in range(order_item.quantity):
            items.append(
                (
                    float(product.length),
                    float(product.width),
                    float(product.height),
                )
            )

    return total_weight, items


def box_can_fit_order(order, box):
    """
    Check whether the selected box can accommodate
    the complete order.
    """

    total_weight, items = calculate_order_requirements(order)

    # First check maximum weight.
    if total_weight > float(box.max_weight):
        return False

    # Then check physical packing.
    return can_pack_items(items, box)


def find_suitable_box(order):
    """
    Find the cheapest box that can accommodate the order.

    Returns:
        Box object or None
    """

    boxes = order._meta.get_field("items")

    # Get all available boxes from the Box model.
    from .models import Box

    suitable_boxes = []

    for box in Box.objects.all():

        if box_can_fit_order(order, box):
            suitable_boxes.append(box)

    if not suitable_boxes:
        return None

    # Cheapest suitable box.
    return min(
        suitable_boxes,
        key=lambda box: float(box.cost)
    )