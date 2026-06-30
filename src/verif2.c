/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   verif2.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rakrouna <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/06/20 14:52:57 by rakrouna          #+#    #+#             */
/*   Updated: 2019/11/23 16:37:09 by rakrouna         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int		pile_len(t_pile *head)
{
	int i;

	i = 0;
	while (head)
	{
		head = head->next;
		i++;
	}
	return (i);
}

int		pile_min(t_pile *p)
{
	int min;

	min = p->x;
	while (p)
	{
		if (p->x < min)
			min = p->x;
		p = p->next;
	}
	return (min);
}

int		pile_max(t_pile *p)
{
	int max;

	max = p->x;
	while (p)
	{
		if (p->x > max)
			max = p->x;
		p = p->next;
	}
	return (max);
}

int		closest_num(t_pile *p, int num)
{
	int pos;
	int cont;
	int dif;

	pos = 0;
	cont = 0;
	if (p)
		dif = ft_abs(p->x - num);
	while (p)
	{
		if (ft_abs(p->x - num) < dif)
		{
			dif = ft_abs(p->x - num);
			pos = cont;
		}
		cont++;
		p = p->next;
	}
	return (pos);
}

int		islarger(char *nb)
{
	int i;
	int pos;

	if (ft_strcmp(nb, "-") == 0)
		return (0);
	pos = (nb[0] != '-');
	if ((int)ft_strlen(nb) < 11 - pos)
		return (0);
	if ((int)ft_strlen(nb) > 11 - pos)
		return (1);
	if (nb[1 - pos] < 50)
		return (0);
	if (nb[1 - pos] > 50)
		return (1);
	if (nb[2 - pos])
	{
		i = ft_atoi(&nb[2 - pos]);
		if (i > 147483648 - pos)
			return (1);
	}
	return (0);
}
