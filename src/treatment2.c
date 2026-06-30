/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   treatment2.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rakrouna <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/06/20 14:52:57 by rakrouna          #+#    #+#             */
/*   Updated: 2019/11/23 16:37:09 by rakrouna         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_pile	*end_node(t_pile *head)
{
	while (head->next)
		head = head->next;
	return (head);
}

void	pass_pile(t_pile **p1, t_pile **p2, int side)
{
	pab(p1, p2, "pb\n", 1);
	if (side > 0)
		rrab(p2, "rrb\n", 1);
}

void	free_pile(t_pile **p)
{
	while (*p)
		pop(p);
}

int		are_left(t_pile *p, int pivot, int ispa, t_pivot v)
{
	int much;

	much = 0;
	while (p)
	{
		if (ispa && v.min <= p->x && p->x < pivot)
			much += 1;
		if (!ispa && p->x >= pivot)
			much += 1;
		p = p->next;
	}
	return (much);
}

int		last_between(t_pile *p, int min, int max)
{
	while (p->next)
		p = p->next;
	return (min < p->x && p->x <= max);
}
